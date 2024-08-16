function showLoading() {
  let helperText = document.getElementById("helperText");
  let loader = document.getElementById("loaderDots");
  let button = document.getElementById("send");
  loader.style.display = "block";
  helperText.textContent = "Processing";
  button.disabled = true;
}

function showResult(data) {
  let helperText = document.getElementById("helperText");
  let loader = document.getElementById("loaderDots");
  let button = document.getElementById("send");
  loader.style.display = "none";
  helperText.textContent = "Click the button to classify the molecule";
  button.disabled = false;
  console.log(data);
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

  const data = {
    smiles: molecule,
  };

  // Send to the backend
  fetch(apiUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response failed");
      }
      return response.json();
    })
    .then((data) => {
      showResult(data);
    });
}
