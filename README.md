# hackme
Vulnerable application for teaching purposes

## Important disclaimer
 
 This application is not secure, running it on your computer might cause 
 serious problems. Don't do it unless you know what you are doing!

## Running the application
### Check out the repository
```
git clone https://github.com/httpPrincess/hackme/
cd hackme
```
### Create virtual environment
```
virtualenv env
source env/bin/activate
```
### Install dependencies
```
pip install -r requirements.txt
```
### Run application
```
./run.py
```
## Docker-based deployment
Alternative way of running the application is based on docker
### Check out the repository
```
git clone https://github.com/httpPrincess/hackme/
cd hackme
```
### Build and run docker image
```
docker build -t hackme/hackme:latest .
docker run -d -p 8080:8080 hackme/hackme 
```
## Verifying deployment
Regardless of the way in which the application has been ran it should be possible
to make a http query
```
curl -X GET 0.0.0.0:8080
```
If you don't get a response (302) for such a query something is wrong with your deployment

## Application vulnerabilities
Application includes (but is not limited) following vulnerabilities:
 1. Open redirect
 2. Cross-site request forgery
 3. Insecure direct object reference
 4. XSS
 5. Injection (various types)
 6. Security configuration 
