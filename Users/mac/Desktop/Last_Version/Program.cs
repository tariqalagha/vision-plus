using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using System;
using Microsoft.OpenApi.Models;
using System.IO;
using Microsoft.Extensions.FileProviders;

var builder = WebApplication.CreateBuilder(args);

// Add services
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddCors();

// Add file provider service
var resourcePath = Path.Combine(Directory.GetCurrentDirectory(), "Resources");
Directory.CreateDirectory(resourcePath);

var app = builder.Build();

// Configure middleware
app.UseStaticFiles(new StaticFileOptions
{
    FileProvider = new PhysicalFileProvider(resourcePath),
    RequestPath = "/resources"
});

// Define routes
app.MapGet("/", () => "Vision+ Medical Imaging System");
app.MapGet("/api/resources", () => Directory.GetFiles(resourcePath));
app.MapGet("/api/health", () => "System is healthy");
app.MapGet("/api/version", () => new { Version = "1.0.0", Developer = "Dr. Tariq Alagha" });
app.MapGet("/api/status", () => new { Status = "Online", Timestamp = DateTime.UtcNow });

app.Run();