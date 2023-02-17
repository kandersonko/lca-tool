function validateForm() {
  let valid = 1;
  console.log("register validateForm called");
  // Get the value of the input fields
  let first_name = document.getElementById("first_name").value;
  let last_name = document.getElementById("last_name").value;
  let affiliation = document.getElementById("affiliation").value;
  let email = document.getElementById("email").value;
  let password = document.getElementById("password").value;
  let confirm_password = document.getElementById("confirm_password").value;

  // Check the first name
  let first_name_Text;
  if (isNaN(first_name) == false) {
    first_name_Text = "Please enter a first name.";
    valid = 0;
  } else {
    var check = first_name.length > 50;
    if (check) {
      first_name_Text = "Entered first name is too long";
      valid = 0;
    } else {
      first_name_Text = "";
    }
  }
  document.getElementById("firstnameErrorMSG").innerHTML = first_name_Text;

  // Check the last name
  let last_name_Text;
  if (isNaN(last_name) == false) {
    last_name_Text = "Please enter a last name.";
    valid = 0;
  } else {
    var check = last_name.length > 50;
    if (check) {
      last_name_Text = "Entered last name is too long";
      valid = 0;
    } else {
      last_name_Text = "";
    }
  }
  document.getElementById("lastnameErrorMSG").innerHTML = last_name_Text;

  // Check the affiliation
  let affiliation_Text;
  if (isNaN(affiliation) == false) {
    affiliation_Text = "Please enter affiliation.";
    valid = 0;
  } else {
    var check = affiliation.length > 255;
    if (check) {
      affiliation_Text = "Entered affiliation is too long";
      valid = 0;
    } else {
      affiliation_Text = "";
    }
  }
  document.getElementById("affiliationErrorMSG").innerHTML = affiliation_Text;

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

  //check confirmed password
  let confirm_password_Text;
  if (isNaN(confirm_password) == false) {
    confirm_password_Text = "Please reenter your password.";
    valid = 0;
  } else {
    var check = confirm_password.length > 255;
    if (check) {
      confirm_password_Text = "Entered password is too long";
      valid = 0;
    } else {
      var check = password !== confirm_password;
      if (check) {
        confirm_password_Text = "Reentered password is not the same";
        valid = 0;
      } else {
        confirm_password_Text = "";
      }
    }
  }
  document.getElementById("confirmpasswordErrorMSG").innerHTML =
    confirm_password_Text;

  if (valid == 1) {
    return true;
  }
  return false;
}
