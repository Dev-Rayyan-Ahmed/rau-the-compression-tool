const { contextBridge, ipcRenderer } = require('electron')
const os = require('os')
const path = require('path')
const Toastify = require('toastify-js')


contextBridge.exposeInMainWorld('os', {
    homedir: () => os.homedir()
})

contextBridge.exposeInMainWorld('path', {
    join: (...args) => path.join(...args)
})

contextBridge.exposeInMainWorld('Toastify', {
    toast: (options) => Toastify(options).showToast()
})


contextBridge.exposeInMainWorld('versions', {
    node: () => process.versions.node,
    chrome: () => process.versions.chrome,
    electron: () => process.versions.electron
    // we can also expose variables, not just functions
})

contextBridge.exposeInMainWorld('ipcRenderer', {
    send: (channel, data) => ipcRenderer.send(channel, data),
    on: (channel, func) => ipcRenderer.on(channel, (event, ...args) => func(...args))
})


contextBridge.exposeInMainWorld('electronAPI', {
    minimize: () => ipcRenderer.send("window:minimize"),
    maximize: () => ipcRenderer.send("window:maximize"),
    close: () => ipcRenderer.send("window:close"),
    openFile: () => ipcRenderer.invoke('dialog:openFile'),
    getFileInfo: (file) => {
        if (file && file.path) {
            return file.path
        }
    },


    // run huffman; returns result object promise
    runHuffman: (scriptPath, option, filePath) =>
        ipcRenderer.invoke('huffman:run', scriptPath, option, filePath),

    // on stdout/stderr events for live progress of python script
    onStdout: (cb) => ipcRenderer.on('huffman:stdout', (_, chunk) => cb(chunk)),
    onStderr: (cb) => ipcRenderer.on('huffman:stderr', (_, chunk) => cb(chunk))
});