function showLoading() {
  let helperText = document.getElementById("helperText");
  let loader = document.getElementById("loaderDots");
  let button = document.getElementById("send");
  loader.style.display = "block";
  helperText.textContent = "Processing";
  button.disabled = true;
}

function showDone() {
  let helperText = document.getElementById("helperText");
  let loader = document.getElementById("loaderDots");
  let button = document.getElementById("send");
  loader.style.display = "none";
  helperText.textContent = "Click the button to classify the molecule";
  button.disabled = false;
}

async function sendMolecule() {
  showLoading();

  let ketcherFrame = document.getElementById("ifKetcher");
  let ketcher = null;

  if ("contentDocument" in ketcherFrame) {
    ketcher = ketcherFrame.contentWindow.ketcher;
  } else {
    // IE7
    ketcher = document.frames["ifKetcher"].window.ketcher;
  }

  // Get the molecule in Smiles format
  const molecule = await ketcher.getSmiles();

  // Send to the backend
  fetch("http://numbersapi.com/random").then((response) => {
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    response.text().then((data) => {
      console.log(data);
      showDone();
    });
  });
}
