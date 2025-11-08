const { spawn } = require('child_process');
const { app, BrowserWindow, Menu, ipcMain, dialog } = require('electron');
const path = require('path');

const isMac = process.platform === 'darwin';
const isDev = process.env.NODE_ENV !== 'production'

// create the main window
function createMainWindow() {
    const mainWindow = new BrowserWindow({
        title: "RAU",
        width: isDev ? 1000 : 500,
        height: 600,
        frame: false,
        titleBarStyle: "hidden",
        transparent: false,
        titleBarOverlay: {
            color: "#0f1117", // background color for overlay area
            symbolColor: "#e3e6ee", // color of window control buttons
            height: 28
        },
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

    mainWindow.loadFile(path.join(__dirname, "./renderer/index.html"));

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


// close perfectly 
app.on('window-all-closed', () => {
    if (!isMac) {
        app.quit()
    }
})