package com.ldleo.mosk

object StealthScript {
    fun generate(seed: Int, vendor: String, renderer: String, userAgent: String): String {
        return """
        (function() {
            try {
                const seed = $seed;

                // 1. WebRTC Shield (Apagado completo de fugas IP)
                window.RTCPeerConnection = undefined;
                window.webkitRTCPeerConnection = undefined;

                // 2. Hardware Specs coherentes
                Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 8, configurable: false });
                Object.defineProperty(navigator, 'deviceMemory', { get: () => 8, configurable: false });
                Object.defineProperty(navigator, 'maxTouchPoints', { get: () => 5, configurable: false });
                Object.defineProperty(navigator, 'platform', { get: () => 'Linux aarch64', configurable: false });

                // 3. WebGL Spoofing (Vendor y Renderer exactos)
                const fakeVendor = "$vendor";
                const fakeRenderer = "$renderer";

                function patchWebGL(proto) {
                    if (!proto) return;
                    const origGetParameter = proto.getParameter;
                    proto.getParameter = function(parameter) {
                        if (parameter === 37445) return fakeVendor;
                        if (parameter === 37446) return fakeRenderer;
                        return origGetParameter.apply(this, arguments);
                    };
                }
                patchWebGL(window.WebGLRenderingContext ? window.WebGLRenderingContext.prototype : null);
                patchWebGL(window.WebGL2RenderingContext ? window.WebGL2RenderingContext.prototype : null);

                // 4. Canvas Noise Injection (Firma matematica unica por Seed)
                const origToDataURL = HTMLCanvasElement.prototype.toDataURL;
                HTMLCanvasElement.prototype.toDataURL = function() {
                    const ctx = this.getContext('2d');
                    if (ctx && this.width > 0 && this.height > 0) {
                        try {
                            const imgData = ctx.getImageData(0, 0, Math.min(this.width, 10), Math.min(this.height, 10));
                            for (let i = 0; i < imgData.data.length; i += 4) {
                                imgData.data[i] = (imgData.data[i] + (seed % 9) + 1) % 256;
                            }
                            ctx.putImageData(imgData, 0, 0);
                        } catch(e) {}
                    }
                    return origToDataURL.apply(this, arguments);
                };

                const origGetImageData = CanvasRenderingContext2D.prototype.getImageData;
                CanvasRenderingContext2D.prototype.getImageData = function() {
                    const res = origGetImageData.apply(this, arguments);
                    if (res && res.data && res.data.length > 0) {
                        for (let i = 0; i < Math.min(res.data.length, 60); i += 4) {
                            res.data[i] = (res.data[i] + (seed % 9) + 1) % 256;
                        }
                    }
                    return res;
                };

                // 5. AudioContext Noise Injection
                const AudioCtx = window.AudioContext || window.webkitAudioContext;
                if (AudioCtx) {
                    const origGetChannelData = AudioBuffer.prototype.getChannelData;
                    AudioBuffer.prototype.getChannelData = function(channel) {
                        const buffer = origGetChannelData.apply(this, arguments);
                        for (let i = 0; i < Math.min(buffer.length, 30); i++) {
                            buffer[i] = buffer[i] + ((seed % 7) * 0.000001);
                        }
                        return buffer;
                    };
                }

                // 6. Camouflage [native code]
                const nativeToString = Function.prototype.toString;
                const customToString = function() {
                    if (this === HTMLCanvasElement.prototype.toDataURL) {
                        return "function toDataURL() { [native code] }";
                    }
                    if (this === CanvasRenderingContext2D.prototype.getImageData) {
                        return "function getImageData() { [native code] }";
                    }
                    return nativeToString.apply(this, arguments);
                };
                Object.defineProperty(Function.prototype, 'toString', {
                    value: customToString,
                    configurable: false,
                    writable: false
                });
            } catch(e) {}
        })();
        """.trimIndent()
    }
}