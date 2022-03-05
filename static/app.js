const BASE_URL = "http://localhost:5000/api";

const cupcakeList = document.querySelector(".cupcakes-list");

function drawCupcake(cupcake) {
  const div = document.createElement("div");
  div.innerHTML = `
    <img src="${cupcake.image}" width="120">
    <p>${cupcake.flavor}/${cupcake.size}/rating:${cupcake.rating}</p>
  `;
  return div;
}

async function retrieveCupcakes() {
  const res = await axios.get(`${BASE_URL}/cupcakes`);
  for (cupcake of res.data.cupcakes) {
    newCupcake = drawCupcake(cupcake);
    cupcakeList.appendChild(newCupcake);
  }
}

retrieveCupcakes();

// form input
const flavor = document.getElementById("form-flavor");
const size = document.getElementById("form-size");
const rating = document.getElementById("form-rating");
const image = document.getElementById("form-image");
const form = document.getElementById("new-cupcake-form");

form.addEventListener("submit", async e => {
  e.preventDefault();
  const res = await axios.post(`${BASE_URL}/cupcakes`, {
    flavor: flavor.value,
    size: size.value,
    rating: rating.value,
  });
  let newCupcake = res.data.cupcake;
  cupcakeList.appendChild(drawCupcake(newCupcake));
});
