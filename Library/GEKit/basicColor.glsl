
uniform sampler2D bgl_DepthTexture;
uniform sampler2D bgl_RenderedTexture;
uniform float bgl_RenderedTextureWidth;
uniform float bgl_RenderedTextureHeight;

uniform float timer;
uniform float brightness;
uniform float contrast;
uniform float saturation;
uniform float gamma;
uniform float noise;
uniform float vignette;

float vignout = 1.5;	//vignetting outer border
float vignin = 0.1;		//vignetting inner border


float width = bgl_RenderedTextureWidth;
float height = bgl_RenderedTextureHeight;
vec2 texCoord = gl_TexCoord[0].xy;

float rand1(in vec2 coord)
{
	float noise = (fract(sin(dot(coord ,vec2(12.9898,78.233*timer))) * 43758.5453));
	return (noise-0.5);
}

void main(void)
{	
	vec4 color = texture2D(bgl_RenderedTexture,texCoord).rgba;

	// brightness
	color.rgb += color.rgb * brightness;

	// contrast
	color.rgb += (color.rgb-vec3(0.5,0.5,0.5)) * contrast;
	
	// color saturation

	// gamma
	color.rgb = pow(color.rgb, vec3(1.0/gamma));

	// noise
	color.rgb += rand1(texCoord) * noise;
	
	// vignette
	float mask = distance(texCoord, vec2(0.5,0.5));
	mask = smoothstep(vignout, vignin, mask);
	mask = clamp(mask,0.0,1.0);
	mask = mix(1.0, mask, vignette);
	color.rgb *= (mask);

	// color balance


	gl_FragColor = color;
}
