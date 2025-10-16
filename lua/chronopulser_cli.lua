io.write("Mode (encode/decode): ")
local mode = io.read():lower()
io.write("Input: ")
local input = io.read()

if mode=="encode" then
    dofile("chronopulse_encoder.lua")
elseif mode=="decode" then
    dofile("chronopulse_decoder.lua")
else
    print("Invalid mode")
end
