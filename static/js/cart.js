var updateBtns = document.getElementsByClassName('update-cart')

for(i=0;i<updateBtns.length;i++){
    updateBtns[i].addEventListener('click',function(){
        var productID= this.dataset.product
        var action=this.dataset.action
        console.log('productID:', productID, 'Action',action )

        console.log('USER:',user)
        if (user == 'AnonymousUser'){
            console.log(' user is not authenticated')
        }else{
            updateUserorder(productID,action)
        }
    })
}

function updateUserorder(productID,action){
    console.log(' user is authenticated sending data..................')

    var url='/update_item/'

    fetch(url,{
        method:'POST',
        headers:{
            'content-type':'application/json',
            'X-CSRFToken' : csrftoken,
        },
        body:JSON.stringify({'productID': productID, 'action':action})
    })
    .then((response) => {
        return response.json();
    })
    .then((data)=>{
        console.log('data:',data)
    })
}