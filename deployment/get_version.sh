#!/bin/bash

npm version | grep -oP "javpy: '\K.+?(?=')"