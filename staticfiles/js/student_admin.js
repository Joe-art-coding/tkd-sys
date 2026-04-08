// Auto-calculate Date of Birth from IC Number
document.addEventListener('DOMContentLoaded', function() {
    // Find the IC number field
    const icField = document.querySelector('#id_ic_number');
    const dobField = document.querySelector('#id_date_of_birth');
    
    if (icField && dobField) {
        icField.addEventListener('blur', function() {
            const ic = icField.value;
            if (ic && ic.length >= 6) {
                const yymmdd = ic.substring(0, 6);
                const yy = yymmdd.substring(0, 2);
                const mm = yymmdd.substring(2, 4);
                const dd = yymmdd.substring(4, 6);
                
                // Convert YY to YYYY (assume 19xx for 00-99)
                let year = 1900 + parseInt(yy);
                const currentYear = new Date().getFullYear();
                
                // If year is > current year - 10, assume 2000+
                if (year > currentYear - 10) {
                    year = 2000 + parseInt(yy);
                }
                
                const dob = `${year}-${mm}-${dd}`;
                dobField.value = dob;
            }
        });
    }
});