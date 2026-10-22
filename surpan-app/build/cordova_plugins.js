
  cordova.define('cordova/plugin_list', function(require, exports, module) {
    module.exports = [
      {
          "id": "cordova-plugin-btprinter.BluetoothPrinter",
          "file": "plugins/cordova-plugin-btprinter/www/BluetoothPrinter.js",
          "pluginId": "cordova-plugin-btprinter",
        "clobbers": [
          "cordova.plugins.btprinter"
        ]
        },
      {
          "id": "cordova-plugin-honeywell-barcode-scanner.HoneywellBarcodeScanner",
          "file": "plugins/cordova-plugin-honeywell-barcode-scanner/www/honeywellBarcodeScanner.js",
          "pluginId": "cordova-plugin-honeywell-barcode-scanner",
        "clobbers": [
          "cordova.plugins.honeywell.barcode"
        ]
        },
      {
          "id": "cordova-plugin-screen-orientation.screenorientation",
          "file": "plugins/cordova-plugin-screen-orientation/www/screenorientation.js",
          "pluginId": "cordova-plugin-screen-orientation",
        "clobbers": [
          "cordova.plugins.screenorientation"
        ]
        },
      {
          "id": "com-darryncampbell-cordova-plugin-intent.IntentShim",
          "file": "plugins/com-darryncampbell-cordova-plugin-intent/www/IntentShim.js",
          "pluginId": "com-darryncampbell-cordova-plugin-intent",
        "clobbers": [
          "intentShim"
        ]
        }
    ];
    module.exports.metadata =
    // TOP OF METADATA
    {
      "com-darryncampbell-cordova-plugin-intent": "2.2.0",
      "cordova-plugin-btprinter": "0.1.0-dev",
      "cordova-plugin-honeywell-barcode-scanner": "0.0.11",
      "cordova-plugin-screen-orientation": "3.0.3"
    };
    // BOTTOM OF METADATA
    });
    