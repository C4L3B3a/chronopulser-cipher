local json = require("dkjson")

local function loadCipher(path)
    local f = assert(io.open(path, "r"))
    local text = f:read("*a")
    f:close()
    return json.decode(text)
end

local function decodeChronoPulse(code, cipher)
    local alphabet = cipher.Alphabet
    local reverse = {}
    for k,v in pairs(alphabet) do reverse[v] = k end
    local symbols = cipher.Symbols

    local result, current = {}, ""
    for i = 1, #code do
        local s = code:sub(i,i)
        if s=="□" or s=="■" then current = current..s
        elseif s=="●" then
            table.insert(result, reverse[current] or "?")
            current=""
        elseif s=="○" then table.insert(result," ")
        elseif s=="•" then table.insert(result,", "); current=""
        elseif symbols[s] then table.insert(result,symbols[s].Represents)
        else table.insert(result,"?")
        end
    end
    if current~="" then table.insert(result, reverse[current] or "?") end
    return table.concat(result)
end

local cipher = loadCipher("../chronopulse.json")
io.write("Enter code to decode: ")
local code = io.read()
print(decodeChronoPulse(code, cipher))
