function showDialog() {
  let dialog = document.getElementById("welcomeDialog");
  dialog.showModal();
}

if (localStorage.getItem("dontShowDialog") !== "true") {
  setTimeout(() => {
    showDialog();
  }, 2000);
}

function closeDialog() {
  const dontShowAgainCheckbox = document.getElementById("dontShow");
  if (dontShowAgainCheckbox.checked) {
    localStorage.setItem("dontShowDialog", "true");
  }
  let dialog = document.getElementById("welcomeDialog");
  dialog.close();
}

function showLoading() {
  let helperText = document.getElementById("helperText");
  let loader = document.getElementById("loaderDots");
  let button = document.getElementById("send");
  let resultDiv = document.getElementById("resultDiv");
  loader.style.display = "block";
  resultDiv.style.display = "none";
  helperText.textContent = "Processing";
  button.disabled = true;
}

function showResult(data) {
  let helperText = document.getElementById("helperText");
  let loader = document.getElementById("loaderDots");
  let button = document.getElementById("send");
  let resultDiv = document.getElementById("resultDiv");
  let predictionTd = document.getElementById("prediction");
  resultDiv.style.display = "block";
  loader.style.display = "none";
  helperText.textContent = "Click the button to classify the molecule";
  button.disabled = false;
  const predictionId = data.prediction_id;
  const predictionClass = data.prediction_class;
  const success = data.success;
  predictionTd.textContent = success
    ? predictionClass + " [" + predictionId + "]"
    : "Unknown";
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
