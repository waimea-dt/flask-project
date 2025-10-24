//=====================================================
//  Utility front-end functions
//=====================================================


// Trigger when page loads...
window.onload = (event) => {

    //--------------------------------------------------
    // Prevent duplicate submission of forms
    //--------------------------------------------------
    document.querySelectorAll('form').forEach(form => {
        // Get the form's submit button or input
        const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]')

        // Only add listener if form has a submit button
        if (submitBtn) {
            // When the form is submitted...
            form.addEventListener('submit', (e) => {
                // Already submitted?
                if (submitBtn.ariaBusy === 'true') {
                    // Prevent re-submit
                    e.preventDefault()
                }
                else {
                    // Show button as busy
                    submitBtn.ariaBusy = 'true'
                }
            })
        }
    })

}

