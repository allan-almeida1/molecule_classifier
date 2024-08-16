async function sendMolecule() {
  let ketcherFrame = document.getElementById("ifKetcher");
  let ketcher = null;

  if ("contentDocument" in ketcherFrame) {
    ketcher = ketcherFrame.contentWindow.ketcher;
  } else {
    // IE7
    ketcher = document.frames["ifKetcher"].window.ketcher;
  }

  const molecule = await ketcher.getSmiles();

  console.log(molecule);
}
