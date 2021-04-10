# AWS Lambda with XGBoost, Scikit-learn, Pandas and Numpy

A demonstration project and template to deploy a AWS Lambda Function with XGBoost, Scikit-learn, Pandas, Numpy and SciPy based on the layers provided by [AWSLambdas.com](https://www.awslambdas.com).

XGBoost is an optimized gradient boosting library designed to be highly efficient, flexible and portable. It implements machine learning algorithms under the Gradient Boosting framework. XGBoost provides a parallel tree boosting (also known as GBDT, GBM) that solve many data science problems in a fast and accurate way.   

Additionally to XGBoost and Scikit-learn, this layer includes NumPy, SciPy, and Pandas. This is the ultimate and most common machine learning bundle that you can now leverage within AWS Lambdas.

# Prerequisite
Before you start, make sure you have installed the latest version of the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
and the [AWS Serverless Application Model (SAM)](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html).

# Get a copy
```
git clone https://github.com/AwsLambdas/aws-lambda-xgboost.git
```

# Guide

* [How to create a XGBoost layer from AWS Lambdas GUI](#one)
* [How to create a XGBoost layer from a zip file](#two)
* [How to create a Lambda with a XGBoost layer attached](#three)

# <a name="one" id="one"></a>How to create a XGBoost layer from AWS Lambdas GUI

Our XGBoost's layer, which includes Scikit-learn, Pandas, Numpy and SciPy as well, is available for purchasing in [AWSLambdas.com](https://www.awslambdas.com/layers/4/aws-lambda-scikit-learn-xgboost-numpy-scipy-python38-layer).

![Place your Order to downlad or deploy the layer directly to AWS](img/buy-layer.png)

Right after the payment, you will be able to click the button "Deploy to AWS".

Enter the region, and credentials with enough permission to create a Lambda layer.

![Deploy to AWS, enter AWS Region, AWS Key, AWS Secret](img/deploy-to-aws-form.png)

Click the button "Create Layer", and your layer will be created in a few seconds. Copy to the clipboard the returned ARN value and follow the instructions: [How to create a Lambda with a XGBoost layer attached](#three)

# <a name="two" id="two"></a>How to create a XGBoost layer from a zip file

Our XGBoost's layer, which includes Scikit-learn, Pandas, Numpy and SciPy as well, is available for purchasing in [AWSLambdas.com](https://www.awslambdas.com/layers/4/aws-lambda-scikit-learn-xgboost-numpy-scipy-python38-layer).

Right after the payment, you will be able to click the "Download" button. Then, copy the zip file to your project clone's root directory.

![Place your Order to downlad or deploy the layer directly to AWS](img/buy-layer.png)

## Set some environment variables
To simplify the process, let's create some environment variables.
```
export AWSL_RUNTIME=python3.8
export AWSL_RAMDOM=$RANDOM-$RANDOM
export AWSL_LAYER_NAME=awslambdas-com-python38-scikit-learn0241-xgboost133
export AWSL_BUCKET=awslambdas-com-$AWSL_RAMDOM
export AWSL_LAYER_PACKAGE=$AWSL_LAYER_NAME.zip
```

## Create a S3 bucket
You need a bucket to store the layer's zip file.
```
aws s3 mb s3://$AWSL_BUCKET
```

## Upload the layer package (zip)
```
aws s3 cp $AWSL_LAYER_PACKAGE s3://$AWSL_BUCKET/$AWSL_LAYER_PACKAGE
```

## Create a Lambda layer
```
aws lambda publish-layer-version \
    --layer-name $AWSL_LAYER_NAME \
    --license-info "MIT" \
    --content S3Bucket=$AWSL_BUCKET,S3Key=$AWSL_LAYER_PACKAGE \
    --compatible-runtimes $AWSL_RUNTIME
```

Copy to the clipboard the value of "LayerVersionArn" from the command response and follow the instructions: [How to create a Lambda with a XGBoost layer attached](#three)

# <a name="three" id="three"></a>How to create a Lambda with a XGBoost layer attached

This project is a ready-to-use template to create and deploy an AWS Lambda using the [AWS Serverless Application Model (SAM)](https://aws.amazon.com/serverless/sam/).   

## Update the template file
Please, review the ***template.yaml*** file. Notice that the template will create two ressources: an API Gateway and a Lambda function.   

Replace the text "PASTE HERE YOUR LAYER ARN" with the ARN previously obtained.

## Set some environment variables
To simplify the process, let's create a couple of environment variables.
```
export AWSL_RAMDOM=$RANDOM-$RANDOM
export AWSL_STACK_NAME=awslambdas-com-lambda-scikit-learn-xgboost
```

## Create a S3 bucket
AWS SAM need this to store some information about the deployment.
```
aws s3 mb s3://$AWSL_STACK_NAME-$AWSL_RAMDOM
```

## Build and deploy the Lambda
The Lambda to be deployed is very simple. It trains a very simple model and makes a prediction. You can see the code in the file: ***src/app.py***
```python
import json
import numpy as np
import pandas as pd
from xgboost import XGBClassifier

def lambda_handler(event, context):
    model = train_xgb_classifier()
    prediction = model.predict(np.array([[7.2, 3.2, 6.0, 1.8]]).reshape((1,-1)))
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Predicting Iris class for [6.4,2.9,4.3,1.3]: {}".format(prediction)
        })
    }
```

Run the following commands to build and deploy the project to AWS:
```
sam build
sam deploy --stack-name $AWSL_STACK_NAME --s3-bucket $AWSL_STACK_NAME-$AWSL_RAMDOM --capabilities CAPABILITY_IAM
```

## Test your Lambda
To test your Lambda, copy the value of the "API URL" from the previous command Outputs and you can call it with ***curl*** or just open it in a browser.
```
curl "API URL"
```

You should see the following response coming from your Lambda:
```json
{"message": "Predicting Iris class for [6.4,2.9,4.3,1.3]: ['Iris-virginica']"}
```

Congratulations! You have now a base Lambda project that you can use to build on top of it.

## Clean-up
Remove the Lambda and Api Gateway
```
aws cloudformation delete-stack --stack-name $AWSL_STACK_NAME
```

Wait a few seconds to allow the previous command to finish. Then, use the following commands to remove the s3 buckets.
```
aws s3 rb s3://$AWSL_STACK_NAME-$AWSL_RAMDOM --force

# If the zip file was used
aws s3 rb s3://$AWSL_BUCKET --force
```