# Project Setup

Follow these steps to set up and run the project.

## Prepare local environment

### Configure environment variables

Create .env file in the root directory by copying the .env.localhost file:
```bash
cp .env_localhost .env 
```

Provide your own values in the .env file:
```env
BASE_FOLDER="/path/to/the/dataset/files"
DATABASE_PATH="/path/to/the/vectore/db/files"
DATABASE_TABLE="TABLE_NAME_OF_YOUR_DB"
```

### Install Ollama
```bash
curl -fsSL https://ollama.com/install.sh | sh
sudo systemctl enable --now ollama
```

### Pull models
```bash
ollama pull llama3.1:8b
ollama pull Losspost/stella_en_1.5b_v5
```

### Install Dependencies
Install all necessary dependencies using pip:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Create the Dataset
Create the dataset:
```bash
make create-dataset
```

## Load Dataset
Load the dataset to vector database:
```bash
make load-dataset
```

## Test RAG
Run the tests for RAG (Retrieval-Augmented Generation):
```bash
make test-rag
```

## Start REST Server
Start the REST server:
```bash
make start-server
```

## Prepare docker environment

### Configure environment variables

Create .env file in the root directory by copying the .env.docker file:
```bash
cp .env_docker .env 
```

### Build docker images
```bash
make compose-build
```

### Start docker images
```bash
make compose-start
```

### Test app
```bash
curl --location 'http://localhost:8001/ask' \
--header 'Content-Type: application/json' \
--data '{"query": "Tell me about security features"}'
```

## Deploy to AWS

Use instance type: g4dn.xlarge

```bash
yum install -y docker
sudo usermod -a -G docker ec2-user
sudo systemctl enable docker --now
sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
```

AWS CDK typescript
```typescript
import {dev} from '../env';
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as iam from "aws-cdk-lib/aws-iam";

export interface DevAiAssistantProps {
    readonly vpc: ec2.IVpc;
    readonly tags: { key: string, value: string }[];
}

export class DevAiAssistant extends cdk.Stack {
    constructor(scope: Construct, id: string, props: DevAiAssistantProps) {
        super(scope, id, {env: dev});

        // Define the IAM role with ECR access
        const ec2Role = new iam.Role(this, 'EC2ECRRole', {
            assumedBy: new iam.ServicePrincipal('ec2.amazonaws.com'),
        });

        // Attach the necessary ECR policy to the role
        ec2Role.addManagedPolicy(iam.ManagedPolicy.fromAwsManagedPolicyName('AmazonEC2ContainerRegistryReadOnly'));

        // AMI with preinstalled nvidia GPU drivers
        const machineImage = ec2.MachineImage.genericLinux({
            'us-east-1': 'ami-0f9bda29a1b2c9dd7',  // Replace with your correct region and AMI ID
        });

        // EC2 Instance
        const instance = new ec2.Instance(this, 'ai-assistant', {
            instanceType: new ec2.InstanceType('g4dn.xlarge'),
            machineImage: machineImage, // Change this based on your AMI requirements
            vpc: props.vpc,
            keyName: 'ai_assistent',
            role: ec2Role,  // Attach the role to the instance
        });

        // User data script to install Docker Compose
        const userData = ec2.UserData.forLinux();
        userData.addCommands(
            'sudo yum update -y',
            'sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose',
            'sudo chmod +x /usr/local/bin/docker-compose',
            'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 117521322591.dkr.ecr.us-east-1.amazonaws.com',
        );

        // Add the user data to the instance
        instance.addUserData(userData.render());

        // Apply tags to the instance
        props.tags.forEach(tag => {
            cdk.Tags.of(instance).add(tag.key, tag.value);
        });
    }
}
```