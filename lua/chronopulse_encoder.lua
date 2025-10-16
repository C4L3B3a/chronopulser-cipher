local json = require("dkjson")

local function loadCipher(path)
    local f = assert(io.open(path, "r"))
    local text = f:read("*a")
    f:close()
    return json.decode(text)
end

local function encodeChronoPulse(text, cipher)
    local alphabet = cipher.Alphabet
    local symbols = {}
    for k, v in pairs(cipher.Symbols) do
        symbols[v.Represents] = k
    end

    local result = {}
    for i = 1, #text do
        local c = text:sub(i,i)
        local upper = c:upper()
        if alphabet[upper] then
            table.insert(result, alphabet[upper].."●")
        elseif c == " " then
            table.insert(result, "○")
        elseif c:match("[,.;:]") then
            table.insert(result, "•")
        elseif symbols[c] then
            table.insert(result, symbols[c])
        else
            table.insert(result, "?")
        end
    end
    return table.concat(result)
end

local cipher = loadCipher("../chronopulse.json")
io.write("Enter text to encode: ")
local text = io.read()
print(encodeChronoPulse(text, cipher))
