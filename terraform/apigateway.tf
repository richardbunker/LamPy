# API Gateway REST API
resource "aws_apigatewayv2_api" "my_api" {
  name          = var.api_name
  protocol_type = "HTTP"
}

# IAM Role for API Gateway
resource "aws_iam_role" "api_gw_role" {
  name = "${var.api_name}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "apigateway.amazonaws.com"
      }
    }]
  })
}

# IAM Policy for API Gateway
resource "aws_iam_policy" "api_gw_policy" {
  name = "api_gw_policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "lambda:InvokeFunction"
        ]
        Effect   = "Allow"
        Resource = aws_lambda_function.my_lambda.arn
      }
    ]
  })
}

# Attach the IAM policy to the API Gateway IAM role
resource "aws_iam_role_policy_attachment" "api_gw_attach" {
  role       = aws_iam_role.api_gw_role.name
  policy_arn = aws_iam_policy.api_gw_policy.arn
}

# API Gateway integration with Lambda
resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id                 = aws_apigatewayv2_api.my_api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.my_lambda.invoke_arn
  integration_method     = "POST"
  payload_format_version = "2.0"
}

# Add the Lambda permission to the API Gateway
resource "aws_lambda_permission" "apigw_lambda_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.my_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.my_api.execution_arn}/*/*"
}

# API Gateway route
resource "aws_apigatewayv2_route" "default_route" {
  api_id    = aws_apigatewayv2_api.my_api.id
  route_key = "ANY /{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

# Default stage for the API Gateway
resource "aws_apigatewayv2_stage" "default_stage" {
  api_id      = aws_apigatewayv2_api.my_api.id
  name        = "$default"
  auto_deploy = true
}

# Custom domain for API Gateway
resource "aws_apigatewayv2_domain_name" "custom_domain" {
  domain_name = var.api_domain_name
  domain_name_configuration {
    certificate_arn = aws_acm_certificate.api_cert.arn
    endpoint_type   = "REGIONAL"
    security_policy = "TLS_1_2"
  }
  depends_on = [aws_acm_certificate_validation.cert_validation]
}

# Base path mapping for the custom domain
resource "aws_apigatewayv2_api_mapping" "custom_domain_mapping" {
  api_id      = aws_apigatewayv2_api.my_api.id
  domain_name = aws_apigatewayv2_domain_name.custom_domain.domain_name
  stage       = aws_apigatewayv2_stage.default_stage.id
}
