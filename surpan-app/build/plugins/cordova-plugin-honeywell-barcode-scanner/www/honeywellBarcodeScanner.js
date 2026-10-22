cordova.define("cordova-plugin-honeywell-barcode-scanner.HoneywellBarcodeScanner", function(require, exports, module) { 
var exec = require('cordova/exec');

module.exports = {
    onBarcodeScanned: function(success, failure){
        return exec(success, failure, "HoneywellBarcodeScannerPlugin", "onBarcodeScanned", []);
    }
};
});