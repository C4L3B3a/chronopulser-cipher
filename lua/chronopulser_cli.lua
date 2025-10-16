-- ==========================================================
-- ChronoPulse Cipher - Encoder/Decoder (Lua)
-- ----------------------------------------------------------
-- Author: Open Source Community
-- License: MIT
--
-- Dependencies: dkjson (for JSON parsing)
-- ==========================================================

local json = require("dkjson")

-- Load Cipher
local function loadCipher(path)
    local f = assert(io.open(path, "r"))
    local text = f:read("*a")
    f:close()
    return json.decode(text)
end

-- Encode text into ChronoPulse symbols
local function encodeChronoPulse(text, cipher)
    local alphabet = cipher.Alphabet
    local symbolMap = {}
    for k, v in pairs(cipher.Symbols) do
        symbolMap[v.Represents] = k
    end

    local result = {}
    for i = 1, #text do
        local c = text:sub(i,i)
        local upper = c:upper()

        if alphabet[upper] then
            table.insert(result, alphabet[upper] .. "●")
        elseif c == " " then
            table.insert(result, "○")
        elseif symbolMap[c] then
            table.insert(result, symbolMap[c])
        else
            table.insert(result, "?")
        end
    end
    return table.concat(result)
end

-- Decode ChronoPulse symbols into text
local function decodeChronoPulse(code, cipher)
    local alphabet = cipher.Alphabet
    local reverse = {}
    for k,v in pairs(alphabet) do reverse[v] = k end
    local symbols = cipher.Symbols

    local result, current = {}, ""
    for i = 1, #code do
        local s = code:sub(i,i)
        if s == "□" or s == "■" then
            current = current .. s
        elseif s == "●" then
            table.insert(result, reverse[current] or "?")
            current = ""
        elseif s == "○" then
            table.insert(result, " ")
        elseif symbols[s] then
            table.insert(result, symbols[s].Represents)
        else
            table.insert(result, "?")
        end
    end
    if current ~= "" then table.insert(result, reverse[current] or "?") end
    return table.concat(result)
end

-- CLI Entry Point
local cipher = loadCipher("chronopulse.json")
io.write("=== ChronoPulse v2 Encoder/Decoder ===\nMode (encode/decode): ")
local mode = io.read():lower()
io.write("Input: ")
local input = io.read()

if mode == "encode" then
    print("\nResult:\n" .. encodeChronoPulse(input, cipher))
elseif mode == "decode" then
    print("\nResult:\n" .. decodeChronoPulse(input, cipher))
else
    print("Invalid mode.")
end

-- By C4L