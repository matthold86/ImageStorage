# AWS Image Processing Pipeline

### Summary:
This repository contains 3 python lambda files that make up an image processing pipeline built in AWS. The pipeline allows a user to upload an image to an S3 bucket via a web application interface and retrieve that image to be displayed on the web application. Although this is a simple task, it is the basic structure for completely automated image upload, storage, and retrieval. The image object is stored in an S3 database and the S3ObjectKey is stored in a DynamoDB database for quick access querying from the web application.

### Cargo Lambda:
Because I'm new to Rust and I'm still learning how to build interconnected microservices in AWS, I decided to first build the image processing pipeline using python lambda functions. Then, once the pipeline is live and deployed, replicate the lambda functions in Rust. This certainly extends the development process, but then I can troubleshoot AWS pipeline issues using a language I'm familiar with (python) and troubleshoot Rust issues after I know the pipeline already works. The python lambda functions shown in this repository are replicated as Cargo Lambda functions and provided in the links below. Because cargo lambda functions require a binary zip file for deployment, all three functions had to be replicated and compiled in separate repositories. Below are the links to the three separate cargo lambda repositories and a brief description of each. 

[s3presignedkey_rust_lambda](https://github.com/matthold86/s3presignedkey_rust_lambda): Retrieve S3 presigned key. <br>
[imagemetadata_rust_lambda](https://github.com/matthold86/imagemetadata_rust_lambda): Monitor S3 bucket; extract and store image S3ObjectKey in DynamoDB. <br>
[retrieveimage_rust_lambda](https://github.com/matthold86/retrieveimage_rust_lambda): Query DynamoDB; retrieve image S3ObjectKey. <br>

*Note: This project is associated with Duke IDS721 Mini Projects 5 and 6. `imagemetadata_rust_lambda` and `retrieveimage_rust_lambda` both interact with a DynamoDB database (MP5). All three cargo lambda functions have Cloudwatch and X-Ray monitoring (MP6).*

### Pipeline Description:
The pipeline starts on a static website (I used my personal website as a demo). When a user uploads an image via the "upload" interface. An http request is sent to the first lambda function `s3bucket-presignkey`. The lambda function requests a presigned upload key from the S3 bucket using an authorized IAM role. The S3 bucket returns a presigned key and the lambda function passes the key back to the static website in the http response. A javascript event handler is then able to use the presigned key to upload the image directly to the S3 bucket. This method was chosen because it utilizes AWS user authentication roles and applys the principle of least privaledge to each entity in the pipeline. 

When the image is uploaded, a second lambda function `extractPhotoMetadata` is triggered by the action of a new upload to the S3 bucket. This trigger is automatic as the ambda function is designed to watch for new uploads into this database to begin the metadata extraction automatically. This lambda function pulls the file path of the image and extracts from the simulated S3 bucket directories, the "bar name" and "Drink Name" as well as the S3ObjectKey that can be used for direct retrieval. The lambda function then stores this metadata in a dynamoDB where the "Bar Name" and "Drink Name" are the partition and sort keys respectively. The S3ObjectKey is an attribute associated with the partition and sort key unique identifier. This completes the image upload pipeline.

Image retrieval pipeline also starts in the static website. From the website, the Drink Name and Bar Name are entered by the user and passed as a json package to a third lambda function which executes a query of the dynamoDB database. The query returns the S3ObjectKey associated with the Bar and Drink name and the lambda function returns the ObjectKey to the static website via the http response. From within the website, the S3ObjectKey can now be used directly to show the image on the website. To see this pipeline, find the video below.

### Demonstration:

https://youtu.be/H9Uebmp_hKY
