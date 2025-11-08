const { spawn } = require('child_process');
const { app, BrowserWindow, Menu, ipcMain, dialog } = require('electron');
const path = require('path');

const isMac = process.platform === 'darwin';
const isDev = process.env.NODE_ENV !== 'production';
const PYTHON_ROOT_DIR = path.join(__dirname, '..')

// create the main window
function createMainWindow() {
    const mainWindow = new BrowserWindow({
        title: "RAU",
        width: isDev ? 1000 : 500,
        height: 600,
        frame: false,
        titleBarStyle: "hidden",
        transparent: false,
        // titleBarOverlay: {
        //     color: "#0f1117", // background color for overlay area
        //     symbolColor: "#e3e6ee", // color of window control buttons
        //     height: 28
        // },
        webPreferences: {
            contextIsolation: true,
            nodeIntegration: true,
            preload: path.join(__dirname, 'preload.js')
        }
    });

    // open dev tool if in dev environment
    if (isDev) {
        mainWindow.webContents.openDevTools();
    }
    mainWindow.setMenuBarVisibility(false)
    mainWindow.loadFile(path.join(__dirname, "./renderer/index.html"));

    // listening the event from render named min max close using inter process communication
    // minimize windows
    ipcMain.on("window:minimize", () => mainWindow.minimize());
    // maximize windows
    ipcMain.on("window:maximize", () => {
        if (mainWindow.isMaximized()) mainWindow.unmaximize();
        else mainWindow.maximize();
    });

    // close window 
    ipcMain.on("window:close", () => mainWindow.close());
}


// app is ready 
app.whenReady().then(() => {
    createMainWindow();

    // implement menu
    // const mainMenu = Menu.buildFromTemplate(menu)
    // Menu.setApplicationMenu(mainMenu)

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows.length === 0)
            createMainWindow()
    })
})

// MENU template
const menu = [
    ...(isMac ? [{
        label: app.name,
        submenu: [{
            label: "About"
        }]
    }] : []),

    {
        role: "fileMenu"
    },

    ...(!isMac ? [{
        label: "help",
        submenu: [{ label: "about", click: () => console.log("create about window") }]
    }] : [])
]
// const menu = [
//     {
//         label: 'File',
//         submenu: [{
//             label: 'Quit',
//             click: () => app.quit(),
//             accelerator: 'CmdOrCtrl+w'
//         }]
//     }
// ]

// response to ipc render 


// Open file dialog and return full path(s)
ipcMain.handle('dialog:openFile', async () => {
    const { canceled, filePaths } = await dialog.showOpenDialog({
        properties: ['openFile'],
        // optionally specify filters: [{ name: 'All Files', extensions: ['*'] }]
    });
    if (canceled) return null;
    const filePath = filePaths[0]
    const fileName = require('path').basename(filePath);

    return { filePath, fileName };
});

// 
ipcMain.handle('huffman:run', async (event, scriptPath, option, filePath) => {
    const promise = new Promise((resolve, rejects) => {

        const command = process.platform === 'win32' ? 'python' : 'python3';
        const args = ['-m', scriptPath, option, filePath];

        // now run a sub process of python script 
        const py = spawn(command, args, { cwd: PYTHON_ROOT_DIR });
        let stdout = '';
        let stderr = '';

        // py is sub process and we are listening its outout so that we can show result on render
        py.stdout.on('data', (data) => {
            stdout += data.toString();
            // forward progress to renderer (one-way)
            event.sender.send('huffman:stdout', data.toString());
        });

        // same with error
        py.stderr.on('data', (data) => {
            stderr += data.toString();
            // forward progress to renderer (one-way)
            event.sender.send('huffman:stderr', data.toString());
        });

        py.on('close', (code) => {
            if (code === 0) {
                resolve({ success: true, stdout })
            } else {
                resolve({ success: false, code, stdout, stderr })
            }
        });

        py.on('error', (err) => {
            rejects({ success: false, error: err.message })
        });

    });

    return promise
})

// close perfectly 
app.on('window-all-closed', () => {
    if (!isMac) {
        app.quit()
    }
})