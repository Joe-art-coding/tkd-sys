// Auto-calculate Date of Birth from IC Number
document.addEventListener('DOMContentLoaded', function() {
    const icField = document.querySelector('#id_ic_number');
    const dobField = document.querySelector('#id_date_of_birth');
    
    if (icField && dobField) {
        icField.addEventListener('blur', function() {
            const ic = icField.value;
            if (ic && ic.length >= 6) {
                const yymmdd = ic.substring(0, 6);
                const yy = parseInt(yymmdd.substring(0, 2));
                const mm = yymmdd.substring(2, 4);
                const dd = yymmdd.substring(4, 6);
                
                const currentYear = new Date().getFullYear();
                
                // Calculate possible years
                const year1900 = 1900 + yy;
                const year2000 = 2000 + yy;
                
                // Choose the year that is not in the future
                let year;
                if (year2000 <= currentYear) {
                    year = year2000;  // 2014, 2005, etc.
                } else {
                    year = year1900;  // 1993, 1998, etc.
                }
                
                const dob = `${year}-${mm}-${dd}`;
                dobField.value = dob;
                
                // Visual feedback
                dobField.style.backgroundColor = '#e8f5e9';
                setTimeout(() => {
                    dobField.style.backgroundColor = '';
                }, 500);
            }
        });
    }
});