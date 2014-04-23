/*
SSAO GLSL shader v1.2
assembled by Martins Upitis (martinsh) (devlog-martinsh.blogspot.com)
original technique is made by Arkano22 (www.gamedev.net/topic/550699-ssao-no-halo-artifacts/)

*/

uniform sampler2D bgl_DepthTexture;
uniform sampler2D bgl_RenderedTexture;
uniform float bgl_RenderedTextureWidth;
uniform float bgl_RenderedTextureHeight;
uniform float timer;

#define PI    3.14159265

float width = bgl_RenderedTextureWidth; //texture width
float height = bgl_RenderedTextureHeight; //texture height

vec2 texCoord = gl_TexCoord[0].st;

//------------------------------------------
//general stuff

//make sure that these two values are the same for your camera, otherwise distances will be wrong.

float znear = 0.1; //Z-near
float zfar = 100.0; //Z-far

//user variables
int samples = 8; //ao sample count

float radius = 5.0; //ao radius
float aoclamp = 0.25; //depth clamp - reduces haloing at screen edges
bool noise = true; //use noise instead of pattern for sample dithering
float noiseamount = 0.001; //dithering amount

float diffarea = 0.4; //self-shadowing reduction
float gdisplace = 0.4; //gauss bell center

float lumInfluence = 0.5; //how much luminance affects occlusion

//--------------------------------------------------------

vec2 rand(vec2 coord) //generating noise/pattern texture for dithering
{
	float noiseX = ((fract(1.0-coord.s*(width/2.0))*0.25)+(fract(coord.t*(height/2.0))*0.75))*2.0-1.0;
	float noiseY = ((fract(1.0-coord.s*(width/2.0))*0.75)+(fract(coord.t*(height/2.0))*0.25))*2.0-1.0;
	
	if (noise)
	{
		noiseX = clamp(fract(sin(dot(coord ,vec2(20.0,46.0*timer))) * 47358.5453),0.0,1.0)*2.0-1.0;
		noiseY = clamp(fract(sin(dot(coord ,vec2(41.0,37.2*timer)*2.0)) * 43758.5453),0.0,1.0)*2.0-1.0;
	}
	return vec2(noiseX,noiseY)*noiseamount;
}


float readDepth(in vec2 coord) 
{
	if (gl_TexCoord[0].x<0.0||gl_TexCoord[0].y<0.0) return 1.0;
	return (2.0 * znear) / (zfar + znear - texture2D(bgl_DepthTexture, coord ).x * (zfar-znear));
}

float compareDepths(in float depth1, in float depth2,inout int far)
{   
	float garea = 2.0; //gauss bell width    
	float diff = (depth1 - depth2)*100.0; //depth difference (0-100)
	//reduce left bell width to avoid self-shadowing 
	if (diff<gdisplace)
	{
	garea = diffarea;
	}else{
	far = 1;
	}
	
	float gauss = pow(2.7182,-2.0*(diff-gdisplace)*(diff-gdisplace)/(garea*garea));
	return gauss;
}   

float calAO(float depth,float dw, float dh)
{   
	float dd = (1.0-depth)*radius;
	
	float temp = 0.0;
	float temp2 = 0.0;
	float coordw = gl_TexCoord[0].x + dw*dd;
	float coordh = gl_TexCoord[0].y + dh*dd;
	float coordw2 = gl_TexCoord[0].x - dw*dd;
	float coordh2 = gl_TexCoord[0].y - dh*dd;
	
	vec2 coord = vec2(coordw , coordh);
	vec2 coord2 = vec2(coordw2, coordh2);
	
	int far = 0;
	temp = compareDepths(depth, readDepth(coord),far);
	//DEPTH EXTRAPOLATION:
	if (far > 0)
	{
		temp2 = compareDepths(readDepth(coord2),depth,far);
		temp += (1.0-temp)*temp2;
	}
	
	return temp;
} 

void main(void)
{
	vec2 noise = rand(texCoord); 
	float depth = readDepth(texCoord);
	
	float w = (1.0 / width)/clamp(depth,aoclamp,1.0)+(noise.x*(1.0-noise.x));
	float h = (1.0 / height)/clamp(depth,aoclamp,1.0)+(noise.y*(1.0-noise.y));
	
	float pw;
	float ph;
	
	float ao;
	
	float dl = PI*(3.0-sqrt(5.0));
	float dz = 1.0/float(samples);
	float l = 0.0;
	float z = 1.0 - dz/2.0;
	
	for (int i = 0; i <= samples; i ++)
	{     
		float r = sqrt(1.0-z);
		
		pw = cos(l)*r;
		ph = sin(l)*r;
		ao += calAO(depth,pw*w,ph*h);        
		z = z - dz;
		l = l + dl;
	}
	
	ao /= float(samples);
	ao = 1.0-ao;	
	

	vec3 color = texture2D(bgl_RenderedTexture,texCoord).rgb;
	
	vec3 lumcoeff = vec3(0.299,0.587,0.114);
	float lum = dot(color.rgb, lumcoeff);
	vec3 luminance = vec3(lum, lum, lum);
	
	vec3 final = vec3(color*mix(vec3(ao),vec3(1.0),luminance*lumInfluence));
	
	gl_FragColor = vec4(final,1.0); 
	
}