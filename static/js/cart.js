// javascripts for handling events on buttons  
var updateBtn = document.getElementsByClassName('update-cart')
// set index to 0, here we are looping through buttons
for(var i=0; i < updateBtn.length; i++)
{
    // for each button add event listener & the type of event is click .
    // on each click the function will execute, here we get product ID and action from frontend as we click button.
        updateBtn[i].addEventListener('click', function(){
        var productID = this.dataset.product
        var action = this.dataset.action
        console.log('productID :',productID, 'action :',action)
        // user is authenticated or not we get this value from main.html.
        console.log('USER :', user)
         if(user == 'AnonymousUser')
         {
            addCookiesItem(productID, action)   
         }
         else
         {                                                                                      
            updateUserOrder(productID, action)
         }
    })
}

 function addCookiesItem(productID, action)
 {
    console.log('Not logged in')
    if(action == 'add')
    {
        if(cart[productID]== undefined) 
        {
            cart[productID]={'quantity':1} // e.g 2: {quantity: 1}, here 2 is productID, 1 is no of quantity.
            console.log('Item added')
        }
        else
        { 
            cart[productID]['quantity'] += 1
            console.log('Item quantity increased')
        }
    }
    if(action=='remove')
    {
        cart[productID]['quantity'] -= 1
        if(cart[productID]['quantity'] <=0)
        {
            console.log('Remove Item')
            delete cart[productID]
        }
    }
    console.log('Cart :', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) 
    location.reload()
 }

function updateUserOrder(productID, action)
{
    console.log('User login , sending data')
    // we want to send the data to update_order
    var url = 'update_order'

    fetch(url, {
        method: 'POST',
        headers:{'ContentType':'application/json',
        'X-CSRFToken': csrftoken
    },
    // using body we will send the data as object to the backend i.e to view.
    // we will send the object to the backend as string.
    // JSON.stringify() --> Convert a JavaScript object into a string 
    body:JSON.stringify({'productID':productID, 'action':action})
    })
    // we have to return promise in response. i.e Item is added from the view.
    .then((response) => {
        return response.json()
    })
    // here we console out the data i.e string value in views.
    .then((data) => {
        console.log('data:', data)
        location.reload() //reload the page once new data get passed in immediatetly
    })
}