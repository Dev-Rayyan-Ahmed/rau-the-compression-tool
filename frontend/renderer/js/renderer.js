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
    updateOutput(chunk)
});
window.electronAPI.onStderr(chunk => {
    updateOutput('ERR: ' + chunk)
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
        outputPath = window.path.dirname(filePath)
        updateOutput(`Selected file: ${fileName} <br> Output file : ${outputPath}`)
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
    const dirName = window.path.dirname(filePath);
    const scriptPath = 'app.main'
    console.log(scriptPath, option, filePath, dirName)
    updateOutput('Starting...\n');

    const resultPromise = window.electronAPI.runHuffman(scriptPath, option, filePath, dirName);

    // live logs already set below via onStdout/onStderr
    const result = await resultPromise;
    console.log(result);
    if (!result.success) {
        if (option == "-c")
            updateOutput("Error: Failed To compress File. Not a text file try again");
        else
            updateOutput("Error: File is not perfect rau file")
    } else {
        updateOutput("Success: File Saved in Folder:" + `${dirName}`);
        selectedFilePath = null;
    }


}

// make sure file is .rau file
function isFileTypeCorrect(file) {
    const acceptedFileType = ['.rau', '*']
    return file && acceptedFileType.includes(file['type']);
}

function alertError(message) {
    window.Toastify.toast({
        text: "⚠️ " + message,  
        duration: 4000,
        close: true,
        gravity: "top",
        position: "center",
        style: {
            background: "#330000",   
            borderLeft: "5px solid #ff3333", 
            color: "#ffcccc",        
            fontSize: "16px",
            // borderRadius: "5px",
            boxShadow: "0 4px 6px rgba(0,0,0,0.3)"
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
