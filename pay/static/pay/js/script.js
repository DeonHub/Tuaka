


const checkOut = (event) => {
    const expire = document.getElementById('expire')

    if(event.checked == false){
            expire.style.display = "block"
    }
    else{
            expire.style.display = "none"
    }
    
}




const loadDuration = (event) => {
        const label = document.getElementById('label')
        const paid = document.getElementById('paid')
        
        const input = document.getElementById('input')
        const total_amount_due = document.getElementById('total_amount_due')

        const amount_paid = document.getElementById('amount_paid')
        const arrears = document.getElementById('arrears')
        const charge = document.getElementById('charge')

        const balance = document.getElementById('balance')

        let charge_percentage = document.getElementById('charge_percentage')


        let payments = document.getElementById('payments')
        
        // let charge = document.getElementById('charge')



        if(event.value != ""){
                payments.style.display = "block"

                if(event.value == "part"){
        
                        // alert("Human")
                        label.style.display = "block"
                        // form_check.style.display = "block"
                        input.style.display = "block"
                        // arrears.style.display = null
                        //paid.value = 0
                        total_amount_due.value = null
        
                        paid.value = ""
                        amount_paid.value = ""
                        arrears.value = ""
                        charge.value = ""
        
                }else if(event.value == "full"){
                        label.style.display = "none"
                        // form_check.style.display = "none"
                        input.style.display = "none"
                        
        
                        total_amount_due.value = parseInt(expiration_bill.value)
                        
                        paid.value = parseInt(total_amount_due.value) - parseInt(balance.value)
        
                        amount_paid.value = paid.value
                      
                        arrears.value = 0
                        var number = parseFloat(amount_paid.value) * parseFloat(charge_percentage.value * 0.01)
                        charge.value = number.toFixed(2)
        
                        // charge.value = parseFloat(amount_paid.value) * parseFloat(charge_percentage.value * 0.01)
                        // arrears.style.display = "none"
                }else{
                        label.style.display = "none"
                        // form_check.style.display = "none"
                        input.style.display = "none"
        
                        // total_amount_due.value = parseInt(expiration_bill.value)
                        // arrears.style.display = "none"
        
                        paid.value = ""
                        total_amount_due.value = ""
                        //balance.value = ""
                        amount_paid.value = ""
                        arrears.value = ""
                        charge.value = ""
        
                }
        
        }else{
                payments.style.display = "none"
        }
     


}



const memberOut = () => {
    // alert("Hello")
    window.localStorage.removeItem('token');
}






function toggle(source) {
    checkboxes = document.getElementsByName('foo[]');
    for(var i=0, n=checkboxes.length;i<n;i++) {
      checkboxes[i].checked = source.checked;
    }
  }



const loadTotal = () => {
    let outstanding_bill = document.getElementById('outstanding_bill')
    let amount = document.getElementById('total_amount_due')
    let expiration_bill = document.getElementById('expiration_bill')
    let renewal_bill = document.getElementById('renewal_bill')

    var testExp = !!document.getElementById("expiration_bill");
    var testRen = !!document.getElementById("renewal_bill");        

    if(testExp === true && testRen === true ){
           if(parseInt(outstanding_bill.value) <= 0){
            amount.value = expiration_bill.value
           }else{
            amount.value = parseInt(expiration_bill.value) + parseInt(renewal_bill.value)       
           }
    }else{
            amount.value = parseInt(outstanding_bill.value)
    }
}



const findArrears = () => {
        let outstanding_bill = document.getElementById('outstanding_bill')
        let amount = document.getElementById('amount_paid')
        let arrears = document.getElementById('arrears')
        let expiration_bill = document.getElementById('expiration_bill')
        let total_amount_due = document.getElementById('total_amount_due')
        let paid = document.getElementById('paid')
        let payment_status = document.getElementById('payment_status')
        let invoice_type = document.getElementById('invoice_type')

        let charge_percentage = document.getElementById('charge_percentage')
        let charge = document.getElementById('charge')
        


        if(invoice_type.value  == "expiry"){
                if(payment_status.value == "part"){

                        // alert("Amount paid should not be less than amount due")
                        
                        if(parseInt(amount.value) >= parseInt(paid.value)){
                                
        
                                   if(parseInt(expiration_bill.value) > 0){
                                        arrears.value = parseInt(expiration_bill.value) - parseInt(amount.value)
                                        if(arrears.value < 0){
                                                arrears.value = 0    
                                        }
                                    }
                                    else{
                                        arrears.value = parseInt(outstanding_bill.value) - parseInt(amount.value)
                                        if(arrears.value < 0){
                                                arrears.value = 0    
                                        }
                                    }
                        }else{
                                alert("Amount paid should not be less than amount due")
                                amount.value = ""       
                                arrears.value = ""       
                        }
                }
                else if(payment_status.value == "full"){
                        if(parseInt(amount.value) < parseInt(paid.value)){
                                alert("Amount paid should not be less than amount due")
                                amount.value = ""
                                arrears.value = "" 
                        }else{
                                arrears.value = 0 
                        } 
                }else{
                        alert("Please select a payment status")
                        amount.value = ""
                }
        }else{
                if (payment_status.value == "full"){
                        if(parseInt(amount.value) < parseInt(paid.value)){
                                alert("Amount paid should not be less than amount due")
                                amount.value = ""
                                arrears.value = "" 
                        } 
                        else{
                                arrears.value = 0
                        }
                }

                else if (payment_status.value == "part"){
                        if(parseInt(amount.value) >= parseInt(paid.value)){
                                
                                arrears.value = parseInt(outstanding_bill.value) - parseInt(amount.value)
                                if(arrears.value < 0){
                                        arrears.value = 0    
                                }
                                    
                        }
                          else{

                                arrears.value = parseInt(outstanding_bill.value) - parseInt(amount.value)
                                if(arrears.value < 0){
                                        arrears.value = 0    
                                }
                                
                                
                                    

                        }
                }  
        }




        if(amount.value == ""){
                charge.value = ""
        }
        else{
                var number = parseFloat(amount.value) * parseFloat(charge_percentage.value * 0.01)
                charge.value = number.toFixed(2)
        }
     

  
}





const checkFunction = () => {
    for(let i=1; i<10; i++){
                let checkBox = document.getElementById("fee_type"+i)
                let amount = document.getElementById("item_amount"+i)

        if (checkBox.checked == true) {
                amount.style.display = "block"
        } else {
                amount.style.display = "none";
            }
        }
    }



const radioCheck = () => {
    for(let i=1; i<5; i++){
            let radio = document.getElementById("install"+i)
            let period = document.getElementById("period")
            let set_date =   document.getElementById("set_pay_date")

            if(radio.checked){
                    amount.disabled = false 

                    if(radio.value == "None"){
                            period.disabled = true    
                            set_date.disabled = false 

                    }
                    else{
                            period.placeholder = `Enter the number of ${radio.value}` 
                            period.disabled = false    
                            set_date.disabled = true       
                    }
            }
            }
} 

const radioCheck2 = (event) => {

        // alert("changed")
        let period = document.getElementById("numver")

        period.placeholder = `Enter the number of ${event.value} to renew for...`
        period.disabled = false    

}


const checkDate = () => {

    let check = document.getElementById('check')

    if(check.checked == true){
            document.getElementById("start_date").disabled = false
            document.getElementById("end_date").disabled = false
    }else{
            document.getElementById("start_date").disabled = true
            document.getElementById("end_date").disabled = true 
    }
}






   