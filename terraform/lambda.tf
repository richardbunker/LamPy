locals {
  lambda_zip_file = "../deployment.zip"
}

# Create Lambda function
resource "aws_lambda_function" "my_lambda" {
  function_name    = var.lambda_function_name
  role             = aws_iam_role.lambda_exec_role.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.12"
  filename         = local.lambda_zip_file
  source_code_hash = filebase64sha256(local.lambda_zip_file)
  architectures    = ["arm64"]

  # Optional: timeout, memory, etc.
  timeout     = 30
  memory_size = 128
}

# IAM Role for Lambda
resource "aws_iam_role" "lambda_exec_role" {
  name = "${var.lambda_function_name}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

# Lambda Cloudwatch IAM Policy
resource "aws_iam_policy" "cloudwatch_policy" {
  name = "lambda_cloudwatch_logs_policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Effect   = "Allow"
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

# Attach the Cloudwatch policy to the Lambda IAM role
resource "aws_iam_role_policy_attachment" "lambda_cloudwatch_logs_attach" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = aws_iam_policy.cloudwatch_policy.arn
}

# Create the Cloudwatch log group
resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/${aws_lambda_function.my_lambda.function_name}"
  retention_in_days = 30
}
