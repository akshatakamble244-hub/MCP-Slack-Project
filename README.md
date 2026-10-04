\## MCP Client Dashboard



The MCP Client Dashboard provides an interactive interface to work with MCP tools.



\### Available Tools



\- Get Weather

\- Send Slack Message

\- Read Slack Messages

\- MCP Server Connection



\## Project Architecture



User

&#x20; |

&#x20; v

MCP Client Dashboard

&#x20; |

&#x20; v

MCP Client

&#x20; |

&#x20; v

MCP Server

&#x20; |

&#x20; +----------------------+

&#x20; |      MCP Tools       |

&#x20; +----------------------+

&#x20; | Weather Tool         |

&#x20; | Slack Send Message   |

&#x20; | Slack Read Messages  |

&#x20; +----------------------+

&#x20; |

&#x20; v

Weather API / Slack API

