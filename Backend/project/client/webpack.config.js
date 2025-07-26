const webpack = require('webpack');
const path = require('path');

const PATHS = {
    app: path.join(__dirname, 'app'),
    build: path.join(__dirname, './js')
};

const config = {
    entry: {
        app: path.join(PATHS.app, 'index.jsx')
    },
    output: {
        path: PATHS.build,
        filename: 'index.js'
    },
    module : {
        loaders : [{
            test : /\.jsx?$/,
            loader : 'babel',
            exclude: /(node_modules|bowercomponents)/,
            include : PATHS.app
        }]
    }
};

module.exports = config;
