#!/bin/bash
#
# This script monitors an AWS AppRunner deployment operation.
# It polls for the status of a specific operation ID.
#

# Exit immediately if a command exits with a non-zero status.
set -eo pipefail

# --- Input Validation ---
SERVICE_ARN=$1
TIMEOUT=${2:-600} # Default to 600 seconds (10 minutes) if not provided

if [ -z "$SERVICE_ARN" ]; then
  echo "::error::Error: Service ARN must be provided as the first argument."
  echo "Usage: $0 <service-arn> [timeout_seconds]"
  exit 1
fi

INTERVAL=20  # Seconds between checks
ELAPSED=0
MAX_CHECKS=$((TIMEOUT / INTERVAL))

echo "Waiting 10 seconds for the new operation to register..."
sleep 10

# --- Retrieve the specific Operation ID ---
# We explicitly filter for the latest CREATE_SERVICE or UPDATE_SERVICE operation.
echo "Searching for the latest CREATE_SERVICE or UPDATE_SERVICE operation..."
OPERATION_ID=$(aws apprunner list-operations \
  --service-arn "$SERVICE_ARN" \
  --query "OperationSummaryList[?Type=='CREATE_SERVICE' || Type=='UPDATE_SERVICE'] | [0].Id" \
  --output text)

if [ -z "$OPERATION_ID" ] || [ "$OPERATION_ID" == "None" ]; then
  echo "::error::Could not retrieve a relevant operation ID (CREATE_SERVICE/UPDATE_SERVICE) for service: $SERVICE_ARN"
  exit 1
fi

echo "Monitoring Operation ID: $OPERATION_ID"
echo "Timeout set to: ${TIMEOUT} seconds."

# --- Monitoring Loop ---
while [ $ELAPSED -lt $TIMEOUT ]; do
  PROGRESS_COUNT=$((ELAPSED / INTERVAL + 1))
  
  # Fetch details for the SPECIFIC operation ID we are monitoring
  # Note: describe-operation is NOT a valid AWS CLI command.
  # We need to use list-operations again and filter by the ID.
  # This is less efficient but more stable across CLI versions.
  OP_DETAILS=$(aws apprunner list-operations --service-arn "$SERVICE_ARN" --query "OperationSummaryList[?Id=='$OPERATION_ID'] | [0]" --output json)

  if [ -z "$OP_DETAILS" ] || [ "$OP_DETAILS" == "None" ]; then
    echo "::warning::Could not retrieve details for operation ID $OPERATION_ID. It might have been removed or is too old."
    sleep $INTERVAL
    ELAPSED=$((ELAPSED + INTERVAL))
    continue
  fi

  OP_STATUS=$(echo "$OP_DETAILS" | jq -r '.Status')
  OP_TYPE=$(echo "$OP_DETAILS" | jq -r '.Type')
  OP_ERROR_MESSAGE=$(echo "$OP_DETAILS" | jq -r '.ErrorMessage') # Get error message directly

  echo "Check $PROGRESS_COUNT / $MAX_CHECKS... Type: $OP_TYPE, Status: $OP_STATUS"
  echo "Debug: OP_STATUS='$OP_STATUS', OP_TYPE='$OP_TYPE'"

  # --- Handle Success ---
  echo "Debug: Checking success condition..."
  if [ "$OP_STATUS" = "SUCCEEDED" ] && ([ "$OP_TYPE" = "UPDATE_SERVICE" ] || [ "$OP_TYPE" = "CREATE_SERVICE" ]); then
    echo "Operation SUCCEEDED. Verifying final service status..."
    # Give AppRunner a moment to stabilize its overall service status after a successful operation
    sleep 15 
    SERVICE_STATUS=$(aws apprunner describe-service --service-arn "$SERVICE_ARN" --query 'Service.Status' --output text)
    echo "Debug: Final service status is '$SERVICE_STATUS'"
    
    if [ "$SERVICE_STATUS" = "RUNNING" ]; then
      echo "Service is RUNNING. Deployment successful!"
      exit 0 # Success!
    elif [ "$SERVICE_STATUS" = "OPERATION_IN_PROGRESS" ]; then
      echo "Service is still OPERATION_IN_PROGRESS. Giving more time..."
      sleep 30
      SERVICE_STATUS=$(aws apprunner describe-service --service-arn "$SERVICE_ARN" --query 'Service.Status' --output text)
      echo "Debug: Service status after extra wait: '$SERVICE_STATUS'"
      if [ "$SERVICE_STATUS" = "RUNNING" ]; then
        echo "Service is now RUNNING. Deployment successful!"
        exit 0 # Success!
      else
        echo "::error::Operation succeeded, but service status is still '$SERVICE_STATUS' after extra wait."
        exit 1 # Failure!
      fi
    else
      echo "::error::Operation succeeded, but final service status is '$SERVICE_STATUS'."
      exit 1 # Failure!
    fi
  fi

  # --- Handle Failures ---
  if [[ "$OP_STATUS" == *"FAILED"* ]] || [ "$OP_STATUS" = "ROLLBACK_SUCCEEDED" ]; then
    if [ "$OP_STATUS" = "ROLLBACK_SUCCEEDED" ]; then
      echo "::warning::Deployment failed and was rolled back."
    else
      echo "::error::Operation FAILED with status: $OP_STATUS."
    fi
    
    # Error message is already in OP_DETAILS from jq -r '.ErrorMessage'
    if [[ "$OP_ERROR_MESSAGE" && "$OP_ERROR_MESSAGE" != "None" && "$OP_ERROR_MESSAGE" != "null" ]]; then
      echo "::error::Error details: $OP_ERROR_MESSAGE"
    fi
    exit 1 # Failure!
  fi

  # --- Handle RollbackInProgress (Optional but good to have) ---
  if [ "$OP_STATUS" = "ROLLBACK_IN_PROGRESS" ]; then
      echo "Deployment is rolling back. Waiting..."
      sleep $INTERVAL
      ELAPSED=$((ELAPSED + INTERVAL))
      continue
  fi

  sleep $INTERVAL
  ELAPSED=$((ELAPSED + INTERVAL))
done

# --- Handle Timeout ---
echo "::error::Timeout: Operation $OPERATION_ID did not complete within ${TIMEOUT} seconds."
exit 1