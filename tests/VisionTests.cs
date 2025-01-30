using Xunit;
using Microsoft.AspNetCore.Mvc.Testing;
using System.Net.Http;
using System.Threading.Tasks;

public class VisionTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly WebApplicationFactory<Program> _factory;

    public VisionTests(WebApplicationFactory<Program> factory)
    {
        _factory = factory;
    }

    [Fact]
    public async Task TestHomePage()
    {
        var client = _factory.CreateClient();
        var response = await client.GetAsync("/");
        Assert.True(response.IsSuccessStatusCode);
    }

    [Fact]
    public async Task TestHealthCheck()
    {
        var client = _factory.CreateClient();
        var response = await client.GetAsync("/api/health");
        Assert.True(response.IsSuccessStatusCode);
    }
}