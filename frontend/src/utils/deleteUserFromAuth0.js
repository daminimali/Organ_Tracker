// utils/deleteUserFromAuth0.js
import fetch from 'node-fetch';

export async function deleteUserFromAuth0(auth0Id) {
  const domain = "dev-o6a67bnmtfoq8kfc.us.auth0.com";
  const clientId = "iywi057Pkru5AGIYbF3VaFVHHjMSF4SV";
  const clientSecret = "EgSE9mO4HSWkaNb3PozmMT3dkRJ4K_8roxxUH2Kpr6YYv4K_Zpo_JleyS2RnH3Wi";
  const audience = `https://${domain}/api/v2/`;

  // Step 1: Get Management API token
  const tokenRes = await fetch(`https://${domain}/oauth/token`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      client_id: clientId,
      client_secret: clientSecret,
      audience,
      grant_type: "client_credentials",
    }),
  });

  const tokenData = await tokenRes.json();
  if (!tokenRes.ok) throw new Error(`Auth0 Token Error: ${tokenData.error_description || tokenData.error}`);

  // Step 2: Call DELETE /api/v2/users/{id}
  const deleteRes = await fetch(`https://${domain}/api/v2/users/${auth0Id}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${tokenData.access_token}`,
    },
  });

  if (!deleteRes.ok) {
    const err = await deleteRes.json();
    throw new Error(`Auth0 Delete Error: ${err.message || err.error}`);
  }
}
