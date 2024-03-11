(num => {
  const div = document.createElement('div');
  const body = document.querySelector('body');
  div.innerText = num;
  body.appendChild(div);
})(3);
