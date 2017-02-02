#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re
import cgi



form="""
<form   method="post">
<h1>Sign Up</h1>
<label for="username">Username</label>
<input type="text" name="username" value="%(username)s"</input>
<span style="color:red;">%(username_error)s</span>
</label>
<br>
<label for="password">Password</label>
<input type="password" name="password"</input>
<span style="color:red;">%(password_error)s</span>
</label>
<br>
<label for="verify">Verify Password</label>
<input type="password" name="verify"</input>
<span style="color:red;">%(password_verify_error)s</span>
</label>
<br>
<label for="email">Email (optional)</label>
<input type="text" name="email" value="%(email)s"</input>
<span style="color:red;">%(email_error)s</span>
</label>
<br>
<input type="submit">
</form>
"""


def valid_username (u_username):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return  USER_RE.match(u_username)

def valid_password (u_password):
    PASS_RE = re.compile(r"^.{3,20}$")
    return PASS_RE.match(u_password)



def valid_email (u_email):
    if u_email!="" :
       EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
       return EMAIL_RE.match(u_email)
    else :
        return True

def verify_passwords(u_password,u_verify) :
    if u_password==u_verify :
       return True


class MainHandler(webapp2.RequestHandler):

      def write_form(self,username="",email="",username_error="", password_error="", password_verify_error="", email_error=""):
          self.response.out.write(form % {"username":username,"email":email,"username_error":username_error,"password_error":password_error,
                                "password_verify_error":password_verify_error,"email_error":email_error})

      def get(self):
          self.write_form()


      def post(self):
          u_username=cgi.escape(self.request.get("username"))
          u_password=cgi.escape(self.request.get("password"))
          u_verify=cgi.escape(self.request.get("verify"))
          u_email=cgi.escape(self.request.get("email"))
          username_error=""
          password_error=""
          password_verify_error=""
          email_error=""

          if not  (valid_username(u_username)) :
             username_error="That's not valid username."
          if not (valid_password(u_password)) :
             password_error="That wasn't a vaild password."
          if not (verify_passwords(u_password,u_verify)) :
             password_verify_error="Your passwords didn't match."
          if not (valid_email(u_email)) :
             email_error="That's not a vaild email."

          if not(valid_username(u_username) and valid_password(u_password) and verify_passwords(u_password,u_verify) and valid_email(u_email)):

             self.write_form(u_username,u_email,username_error,password_error,password_verify_error,email_error)
          else :
                self.redirect('/welcome?username=' +u_username)


class WelcomeHandler(webapp2.RequestHandler):
      def get(self) :
          u_username=self.request.get('username')
          success_content="<p>"+"<strong>"+"Welcome, "+u_username+"!"+"</strong>"+"</p>"
          self.response.write(success_content)


app = webapp2.WSGIApplication([('/', MainHandler),
('/welcome',WelcomeHandler)],debug=True)
