function validateForm() {
  let valid = 1;
  console.log("login validateForm called");
  // Get the value of the input fields
  let email = document.getElementById("email").value;
  let password = document.getElementById("password").value;

  // Check the email
  let email_Text;
  if (isNaN(email) == false) {
    email_Text = "Please enter your email.";
    valid = 0;
  } else {
    var check = email.includes("@");
    if (check == false) {
      email_Text = "Please enter a valid email.";
      valid = 0;
    } else {
      var check = email.length > 100;
      if (check) {
        emailText = "Entered email is too long";
        valid = 0;
      } else {
        email_Text = "";
      }
    }
  }
  document.getElementById("emailErrorMSG").innerHTML = email_Text;

  // check password
  let password_Text;
  if (isNaN(password) == false) {
    password_Text = "Please enter your password.";
    valid = 0;
  } else {
    var check = password.length > 255;
    if (check) {
      password_Text = "Entered password is too long";
      valid = 0;
    } else {
      password_Text = "";
    }
  }
  document.getElementById("passwordErrorMSG").innerHTML = password_Text;

  if (valid == 1) {
    return true;
  }
  return false;
}
