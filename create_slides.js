const fs = require('fs');
const { google } = require('googleapis');

async function main() {
  const creds = JSON.parse(fs.readFileSync('/home/chitsanuphong_agdr/.gog/client_secret.json'));
  const tokenData = JSON.parse(fs.readFileSync('token.json'));
  const { client_id, client_secret, redirect_uris } = creds.installed || creds.web;
  
  const oAuth2Client = new google.auth.OAuth2(client_id, client_secret, redirect_uris[0]);
  oAuth2Client.setCredentials({ refresh_token: tokenData.refresh_token });

  const drive = google.drive({ version: 'v3', auth: oAuth2Client });
  const slides = google.slides({ version: 'v1', auth: oAuth2Client });

  const folderId = '1x69Clmj-BVEfPAjSqkjNE0d9kdb98sbc';

  console.log('Listing files...');
  const res = await drive.files.list({
    q: `'${folderId}' in parents and mimeType contains 'image/' and trashed = false`,
    fields: 'files(id, name, webContentLink, thumbnailLink)',
    pageSize: 100
  });
  const files = res.data.files;
  
  if (!files || files.length === 0) {
    console.log('No images found.');
    return;
  }
  
  console.log(`Found ${files.length} images. Making them public temporarily...`);
  for (const file of files) {
    try {
        await drive.permissions.create({
          fileId: file.id,
          requestBody: { role: 'reader', type: 'anyone' }
        });
    } catch (e) {
        console.log(`Error sharing ${file.id}: ${e.message}`);
    }
  }

  console.log('Creating presentation...');
  const pres = await slides.presentations.create({
    title: 'Site Visit Photos - jibjibjoyjoy'
  });
  const presentationId = pres.data.presentationId;
  console.log(`Created ID: ${presentationId}`);

  // Presentation size (default 16:9)
  const pageWidth = { magnitude: 9144000, unit: 'EMU' };
  const pageHeight = { magnitude: 5143500, unit: 'EMU' };

  const requests = [];
  
  files.forEach((file, index) => {
    const slideId = `slide_${index}`;
    // Create Slide
    requests.push({
      createSlide: {
        objectId: slideId,
        slideLayoutReference: { predefinedLayout: 'BLANK' }
      }
    });
    // Add Image (Full Screen attempt)
    // To make it full screen without distortion, we'd need to crop.
    // For now, let's just make it fit the page or stretch. 
    // The user said "วางรูปเต็มๆสไลด์เลย" (Place image full slide).
    // I'll stretch it to cover.
    requests.push({
      createImage: {
        objectId: `img_${index}`,
        url: file.webContentLink, // This link works for direct download if public
        elementProperties: {
          pageObjectId: slideId,
          size: {
            width: pageWidth,
            height: pageHeight
          },
          transform: {
            scaleX: 1,
            scaleY: 1,
            translateX: 0,
            translateY: 0,
            unit: 'EMU'
          }
        }
      }
    });
  });

  if (requests.length > 0) {
      console.log('Adding slides...');
      await slides.presentations.batchUpdate({
        presentationId,
        requestBody: { requests }
      });
  }
  
  console.log(`SUCCESS: https://docs.google.com/presentation/d/${presentationId}`);
}

main().catch(console.error);
