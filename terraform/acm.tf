# Obtain an SSL certificate from AWS ACM
resource "aws_acm_certificate_validation" "cert_validation" {
  certificate_arn         = aws_acm_certificate.api_cert.arn
  
  # Iterate over the domain validation options and get the fqdn for each validation record
  validation_record_fqdns = [
    for dvo in aws_acm_certificate.api_cert.domain_validation_options : aws_route53_record.validation[dvo.domain_name].fqdn
  ]
}

# Obtain an SSL certificate from AWS ACM
resource "aws_acm_certificate" "api_cert" {
  domain_name       = var.api_domain_name
  validation_method = "DNS"
}
