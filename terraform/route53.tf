# Route 53 hosted zone for the custom domain
data "aws_route53_zone" "hosted_zone" {
  name = var.domain_name
}

# Route 53 DNS record for the custom domain
resource "aws_route53_record" "custom_domain" {
  zone_id = data.aws_route53_zone.hosted_zone.zone_id
  name    = var.api_domain_name
  type    = "A"
  alias {
    name                   = aws_apigatewayv2_domain_name.custom_domain.domain_name_configuration[0].target_domain_name
    zone_id                = aws_apigatewayv2_domain_name.custom_domain.domain_name_configuration[0].hosted_zone_id
    evaluate_target_health = false
  }
}

# DNS validation record using Route 53
resource "aws_route53_record" "validation" {
  for_each = {
    for dvo in aws_acm_certificate.api_cert.domain_validation_options : dvo.domain_name => {
      name  = dvo.resource_record_name
      type  = dvo.resource_record_type
      value = dvo.resource_record_value
    }
  }

  name    = each.value.name
  type    = each.value.type
  zone_id = data.aws_route53_zone.hosted_zone.zone_id
  records = [each.value.value]
  ttl     = 60
}
