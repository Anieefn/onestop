avoid_default =(event) => {
    console.log("Function called");
    event.preventDefault();
    document.querySelector('form').submit();
}