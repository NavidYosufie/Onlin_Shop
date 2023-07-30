function warning(){
    $.get('').then(response =>{
        alert('This page is only a sample and does not have any activity')
    })
}


    function applyFilters() {
        // کد برای اعمال فیلترها و نمایش محصولات

        // مقادیر فیلترها را از صفحه خوانده و در متغیرها ذخیره کنید
        const filterValue1 = document.getElementById('min_price').value;
        const filterValue2 = document.getElementById('max_price').value;
        const filterValue3 = document.getElementById('color-1').value;
        const filterValue4 = document.getElementById('color-2').value;
        const filterValue5 = document.getElementById('color-3').value;
        const filterValue6 = document.getElementById('color-4').value;
        const filterValue7 = document.getElementById('color-5').value;
        const filterValue8 = document.getElementById('size-1').value;
        const filterValue9 = document.getElementById('size-2').value;
        const filterValue10 = document.getElementById('size-3').value;
        const filterValue11 = document.getElementById('size-4').value;
        const filterValue12 = document.getElementById('size-5').value;
        // مقادیر فیلترها را در Local Storage ذخیره کنید
        localStorage.setItem('min_price', filterValue1);
        localStorage.setItem('max_price', filterValue2);
        localStorage.setItem('color-1', filterValue3);
        localStorage.setItem('color-2', filterValue4);
        localStorage.setItem('color-3', filterValue5);
        localStorage.setItem('color-4', filterValue6);
        localStorage.setItem('color-5', filterValue7);
        localStorage.setItem('size-1', filterValue8);
        localStorage.setItem('size-2', filterValue9);
        localStorage.setItem('size-3', filterValue10);
        localStorage.setItem('size-4', filterValue11);
        localStorage.setItem('size-5', filterValue12);
    }

    // صفحه را هنگام لود بازیابی مقادیر فیلترها از Local Storage و اعمال آنها
    window.onload = function () {
        const filterValue1 = localStorage.getItem('min_price');
        const filterValue2 = localStorage.getItem('max_price');
        const filterValue3 = localStorage.getItem('color-1');
        const filterValue4 = localStorage.getItem('color-2');
        const filterValue5 = localStorage.getItem('color-3');
        const filterValue6 = localStorage.getItem('color-4');
        const filterValue7 = localStorage.getItem('color-5');
        const filterValue8 = localStorage.getItem('size-1');
        const filterValue9 = localStorage.getItem('size-2');
        const filterValue10 = localStorage.getItem('size-3');
        const filterValue11 = localStorage.getItem('size-4');
        const filterValue12 = localStorage.getItem('size-5');

        if (filterValue1) {
            document.getElementById('mim_price').value = filterValue1;
            // کد برای اعمال فیلتر
        }
        if (filterValue2) {
            document.getElementById('max_price').value = filterValue2;
            // کد برای اعمال فیلتر
        }
        if (filterValue3) {
            document.getElementById('color-1').value = filterValue3;
            // کد برای اعمال فیلتر
        }
        if (filterValue4) {
            document.getElementById('color-2').value = filterValue4;
            // کد برای اعمال فیلتر
        }
        if (filterValue5) {
            document.getElementById('color-3').value = filterValue5;
            // کد برای اعمال فیلتر
        }
        if (filterValue6) {
            document.getElementById('color-4').value = filterValue6;
            // کد برای اعمال فیلتر
        }
        if (filterValue7) {
            document.getElementById('color-5').value = filterValue7;
            // کد برای اعمال فیلتر
        }
        if (filterValue8) {
            document.getElementById('size-1').value = filterValue8;
            // کد برای اعمال فیلتر
        }
        if (filterValue9) {
            document.getElementById('size-2').value = filterValue9;
            // کد برای اعمال فیلتر
        }
        if (filterValue10) {
            document.getElementById('size-3').value = filterValue10;
            // کد برای اعمال فیلتر
        }
         if (filterValue11) {
            document.getElementById('size-4').value = filterValue11;
            // کد برای اعمال فیلتر
        }
          if (filterValue112) {
            document.getElementById('size-5').value = filterValue12;
            // کد برای اعمال فیلتر
        }


    };
