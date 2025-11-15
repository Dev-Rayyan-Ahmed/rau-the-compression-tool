const fileInput = document.getElementById("fileInput");
const chooseFileBtn = document.getElementById("chooseFileBtn");
const dropZone = document.getElementById("dropZone");
const compressBtn = document.getElementById("compressBtn");
const decompressBtn = document.getElementById("decompressBtn");
const progressBar = document.getElementById("progressBar");
const progressContainer = document.getElementById("progressContainer");
const output = document.getElementById("output");
let selectedFilePath = null;
let outputPath = null;


console.log(versions.node())


// actual event 
compressBtn.addEventListener('click', (e, option = "-c") => runCompression(e, option));
decompressBtn.addEventListener('click', (e, option = "-d") => runCompression(e, option));
chooseFileBtn.addEventListener('click', loadFile);
dropZone.addEventListener("drop", dropFile);



// for changing border color 
dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.style.borderColor = "#4f8cff";
});

dropZone.addEventListener("dragleave", () => {
    dropZone.style.borderColor = "";
});





// for live logs
// just like window.addEventListener
window.electronAPI.onStdout(chunk => {
    log.textContent += chunk;
});
window.electronAPI.onStderr(chunk => {
    log.textContent += 'ERR: ' + chunk;
});

// for min max and close control
document.getElementById("min-btn").addEventListener("click", () => {
    window.electronAPI.minimize();
});

document.getElementById("max-btn").addEventListener("click", () => {
    window.electronAPI.maximize();
});

document.getElementById("close-btn").addEventListener("click", () => {
    window.electronAPI.close();
});


function updateOutput(msg) {
    output.innerHTML = `<p>${msg}</p>`;
}

async function loadFile(e) {
    const { fileName, filePath } = await window.electronAPI.openFile();
    if (filePath) {
        selectedFilePath = filePath; // full path
        outputPath = window.path.join(os.homedir(), 'compressed-file')
        updateOutput(`Selected file: ${fileName} Output file : ${outputPath}`)
    }
}


async function dropFile(e) {
    e.preventDefault();
    dropZone.style.borderColor = "";
    const selectedFile = e.dataTransfer.files[0];
    selectedFilePath = window.electronAPI.getFileInfo(selectedFile)
    updateOutput(`Selected file: ${selectedFilePath}`);
}


async function runCompression(e, option) {
    const filePath = selectedFilePath;
    if (!filePath) return alertError("select a file first")
    const scriptPath = 'app.main'
    updateOutput('Starting...\n');

    const resultPromise = window.electronAPI.runHuffman(scriptPath, option, filePath);

    // live logs already set below via onStdout/onStderr
    const result = await resultPromise;
    if (!result.success) {
        updateOutput("Error: Failed To compress File. try again");
    }

    updateOutput("Success: File Saved in Folder:" + `${outputPath}`);
    selectedFilePath = null;

}

// make sure file is .rau file
function isFileTypeCorrect(file) {
    const acceptedFileType = ['.rau', '*']
    return file && acceptedFileType.includes(file['type']);
}

function alertError(message) {
    Toastify.toast({
        text: message,
        duration: 5000,
        close: false,
        style: {
            background: "red",
            color: "white",
            textAlign: 'center'
        }
    });
}

function alertSuccess(message) {
    Toastify.toast({
        text: message,
        duration: 5000,
        close: false,
        style: {
            background: "green",
            color: "white",
            textAlign: 'center'
        }
    });
}
