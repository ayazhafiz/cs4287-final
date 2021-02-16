# Deployment Instructions

```
aws cloudformation update-stack --stack-name ProdVPC --template-body file://cloudformation/network.yaml --region us-west-2
aws cloudformation update-stack --stack-name PublicSubnetProxies --template-body file://cloudformation/public_proxies.yaml --region us-west-2
aws cloudformation update-stack --stack-name SecurityGroups --template-body file://cloudformation/security_groups.yaml --region us-west-2
```
