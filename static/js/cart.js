const updateBtns = document.querySelectorAll('.update-cart');

for (let i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener('click', function() {
    let productId = this.dataset.product;
    let action = this.dataset.action;
    console.log('product id: ',productId, 'action', action);

    console.log('USER', user);

    if (user === 'AnonymousUser') {
      addCookieItem(productId, action);
    } else {
      updateUserOrder(productId, action);
    }
  });
}

const updateUserOrder = (productId, action) => {
  const url = '/add-to-cart'
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    },
    body: JSON.stringify({'productId': productId, 'action': action})
  })
  .then(res => {
    return res.json();
  })
  .then(data => {
    console.log('Response', data);
    window.location.reload();
  })
  .catch(err => console.log(err));
}


const addCookieItem = (productId, action) => {
  console.log('User is not authenticated');

  if (action === 'add') {
    if (cart[productId] === undefined) {
      cart[productId] = {quantity: 1}
    } else {
      cart[productId]['quantity'] += 1;
    }
  }

  if (action === 'remove') {
    cart[productId]['quantity'] -= 1;

    if (cart[productId]['quantity'] <= 0) {
      console.log('remove item');
      delete cart[productId];
    }
  }

  document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";
  location.reload();
}

console.log(cart);