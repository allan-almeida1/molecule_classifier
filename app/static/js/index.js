/**
 * Show a welcome dialog to the user on the home page
 */
function showDialog() {
  let dialog = document.getElementById("welcomeDialog");
  dialog.showModal();
}

/**
 * Verify local storage for the `dontShowDialog` flag.
 *
 * If it's not found, show the dialog
 */
if (localStorage.getItem("dontShowDialog") !== "true") {
  setTimeout(() => {
    showDialog();
  }, 2000);
}

/**
 * Close the welcome dialog.
 *
 * It the checkbox is checked, set an item in local storage to prevent
 * the dialog to show up again
 */
function closeDialog() {
  const dontShowAgainCheckbox = document.getElementById("dontShow");
  if (dontShowAgainCheckbox.checked) {
    localStorage.setItem("dontShowDialog", "true");
  }
  let dialog = document.getElementById("welcomeDialog");
  dialog.close();
}

/**
 * Change the visibility and content of UI elements to show the request
 * is bein processed
 */
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

/**
 * @typedef {Object} PredictResponse
 * @property {boolean} success Whether the prediction was successful.
 * @property {number} prediction_id The ID of the predicted class.
 * @property {string} prediction_class The name of the predicted class.
 */

/**
 *
 * @param {PredictResponse} data The server's JSON response
 * `success`
 */
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

/**
 * Get the molecule SMILES from Ketcher app and send it to the server.
 *
 * Once the response has been received, display it on the page
 */
async function sendMolecule() {
  showLoading();

  // Get Ketcher object
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

  // Prepare the data
  const data = {
    smiles: molecule,
  };

  /**
   * Send to the server
   *
   * @note `apiUrl` is dinamically obtained in base.html template
   */
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
