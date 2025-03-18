function valid(event){
    console.log("Function called");
    const Inputpass = document.getElementById('password');
    const InputpassValue = Inputpass.value;
    const Inputadd = document.getElementById('address');
    const InputaddValue = Inputadd.value;
    const Inputpho = document.getElementById('phone');
    const InputphoValue = Inputpho.value;
    event.preventDefault();

    const passwordRegex = /^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{9,}$/;

    if (!passwordRegex.test(InputpassValue)) {
        alert("password should be 8 characters 1 symbol and 1 number")
        return;
    }

    if(InputphoValue === '' || InputphoValue[0] === 0  ){
        alert ("please enter a valid number");
        return;
    }

    if (InputaddValue === '' || InputaddValue.length <= 8) {
        alert("Enter the valid address");
        return;
    }

    console.log("All validations passed. Submitting the form...");
    document.querySelector('form').submit();
}