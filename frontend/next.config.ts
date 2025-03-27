import type { NextConfig } from "next";
const fs = require("fs");
const https = require("https");

const nextConfig: NextConfig = {
  images: {
    domains: ["localhost"], // If you want to load images from localhost
  },

  devServer: {
    https: {
      key: fs.readFileSync("../conf/key.key"), // Path to your private key
      cert: fs.readFileSync("../conf/crt.crt"), // Path to your certificate
    },
  },
};

module.exports = nextConfig;
