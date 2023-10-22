# Auth flow
## 1. Create verifications bound to an email
   * `PUT /auth/verifications`
     * 204 response
   * send list of emails to verify
     * optionally add users id 
   * if this endpoint is protected the system is in invite only mode
     * no auth or bearer auth
## 2. Get information about the verification 
   * `GET /auth/verifications/:verification`
     * if a user id was specified in step 1 indicate that the user needs to be logged in instead of registering
   * this step is optional
   * will be done by frontend to figure out which email the verification is valid for
   * no auth
## 3. Connect email with a user
   * `POST /auth/:verification`
     * if user was not specified in step 1 force the use of POST
     * no auth
   * `PATCH /auth/something`
     * if user was specified in step 1 force the use of PATCH
     * bearer auth
   
  
## new 
* user defines password before email is verified but a verified email is required to log in.
* update the Auth flow above to reflect this