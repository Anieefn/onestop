function valid(event){
    console.log("Function called");
    const Inputpass = document.getElementById('password');
    const InputpassValue = Inputpass.value;
    const Inputadd = document.getElementById('address');
    const InputaddValue = Inputadd.value;
    const Inputpho = document.getElementById('phone');
    const InputphoValue = Inputpho.value;
    const Inputname = document.getElementById('name');
    const InputnameValue = Inputname.value;
    const Inputemail = document.getElementById('email');
    const InputemailValue = Inputname.value;
    event.preventDefault();

    const passwordRegex = /^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{9,}$/;

    if (!passwordRegex.test(InputpassValue)) {
        alert("password should be 8 characters 1 symbol and 1 number")
        return;
    }

    if (!InputemailValue) {
        alert("Enter the username");
        return;
    }
    

    if (!InputaddValue || InputaddValue.length <= 8) {
        alert("Enter the valid address");
        return;
    }
    if (InputphoValue[0] === 0) {
        alert("Enter a vaild number")
        return
    }
    if (!InputphoValue) {
        alert("Enter the modile number");
        return;
    }
    

    if (!InputemailValue) {
        alert("Enter the email");
        return;
    }

    console.log("All validations passed. Submitting the form...");
    document.querySelector('form').submit();
}